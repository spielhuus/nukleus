import os
import platform
import logging
from ctypes import (CDLL, CFUNCTYPE, Structure, c_int, c_char_p, c_void_p,
                    c_bool, c_double, POINTER, c_short)
from ctypes.util import find_library
import numpy as np

logger = logging.getLogger(__name__)

captured_output = []


class ngcomplex(Structure):
    _fields_ = [
        ('cx_real', c_double),
        ('cx_imag', c_double)]


class vector_info(Structure):
    _fields_ = [
        ('v_name', c_char_p),
        ('v_type', c_int),
        ('v_flags', c_short),
        ('v_realdata', POINTER(c_double)),
        ('v_compdata', POINTER(ngcomplex)),
        ('v_length', c_int)]


class dvec_flags(object):
    vf_real = (1 << 0)  # The data is real.
    vf_complex = (1 << 1)  # The data is complex.
    vf_accum = (1 << 2)  # writedata should save this vector.
    vf_plot = (1 << 3)  # writedata should incrementally plot it.
    vf_print = (1 << 4)  # writedata should print this vector.
    vf_mingiven = (1 << 5)  # The v_minsignal value is valid.
    vf_maxgiven = (1 << 6)  # The v_maxsignal value is valid.
    vf_permanent = (1 << 7)  # Don't garbage collect this vector.


class vecvalues(Structure):
    _fields_ = [
        ('name', c_char_p),
        ('creal', c_double),
        ('cimag', c_double),
        ('is_scale', c_bool),
        ('is_complex', c_bool)]


class vecvaluesall(Structure):
    _fields_ = [
        ('veccount', c_int),
        ('vecindex', c_int),
        ('vecsa', POINTER(POINTER(vecvalues)))]


@CFUNCTYPE(c_int, c_char_p, c_int, c_void_p)
def printfcn(output, _id, _ret):
    """Callback for libngspice to print a message"""
    logger.debug(f"printcfn {id} {_ret} {output}")
    global captured_output
    prefix, _, content = output.decode('ascii').partition(' ')
    if prefix == 'stderr':
        logger.error(content)
    else:
        captured_output.append(content)
    return 0


@CFUNCTYPE(c_int, c_char_p, c_int, c_void_p)
def statfcn(status, _id, _ret):
    """
    Callback for libngspice to report simulation status like 'tran 5%'
    """
    logger.warn(status.decode('ascii'))
    return 0


@CFUNCTYPE(c_int, c_int, c_bool, c_bool, c_int, c_void_p)
def controlled_exit(exit_status, immediate_unloading, requested_exit,
                    libngspice_id, ret):
    logger.warn('ControlledExit',
                dict(exit_status=exit_status,
                     immediate_unloading=immediate_unloading,
                     requested_exit=requested_exit,
                     ibngspice_id=libngspice_id, ret=ret))


@CFUNCTYPE(c_int, POINTER(vecvaluesall), c_int, c_int, c_void_p)
def send_data(self, vecvaluesall_, num_structs, libngspice_id, ret):
    logger.warn('SendData', dict(vecvaluesall=vecvaluesall_,
                                 num_structs=num_structs,
                                 libngspice_id=libngspice_id,
                                 ret=ret))


class ngspice():
    def __init__(self):
        if os.name == 'nt':  # Windows
            # http://stackoverflow.com/a/13277363
            curr_dir_before = os.getcwd()

            drive = os.getenv("SystemDrive") or 'C:'

            # Python and DLL must both be same number of bits
            if platform.architecture()[0] == '64bit':
                spice_path = os.path.join(drive, os.sep, 'Spice64')
            elif platform.architecture()[0] == '32bit':
                spice_path = os.path.join(drive, os.sep, 'Spice')
            else:
                raise RuntimeError(
                    "Couldn't determine if Python is 32-bit or 64-bit")

            """
            https://sourceforge.net/p/ngspice/discussion/133842/thread/1cece652/#4e32/5ab8/9027
            On Windows, when environment variable SPICE_LIB_DIR is empty, ngspice
            looks in `C:\Spice64\share\ngspice\scripts`.  If the variable is not empty
            it tries `%SPICE_LIB_DIR%\scripts\spinit`
            """

            if 'SPICE_LIB_DIR' not in os.environ:
                os.environ['SPICE_LIB_DIR'] = os.path.join(
                    spice_path, 'share', 'ngspice')
            os.chdir(os.path.join(spice_path, 'bin_dll'))
            self.spice = CDLL('ngspice')
            os.chdir(curr_dir_before)
        else:  # Linux, etc.
            try:
                lib_location = os.environ['LIBNGSPICE']
            except KeyError:
                lib_location = find_library('ngspice')
            self.spice = CDLL(lib_location)

        # int  ngSpice_Command(char* command);
        self.spice.ngSpice_Command.argtypes = [c_char_p]

        # int ngSpice_Circ(char**)
        self.spice.ngSpice_Circ.argtypes = [POINTER(c_char_p)]
        self.spice.ngSpice_AllPlots.restype = POINTER(c_char_p)

        self.spice.ngSpice_AllVecs.argtypes = [c_char_p]
        self.spice.ngSpice_AllVecs.restype = POINTER(c_char_p)
        self.spice.ngSpice_CurPlot.restype = c_char_p

        self.spice.ngSpice_Init(printfcn, statfcn,
                                controlled_exit, send_data,
                                None, None, None)
        # Prevent paging output of commands (hangs)
        # /* get info about a vector */
        # pvector_info ngGet_Vec_Info(char* vecname);
        self.spice.ngGet_Vec_Info.restype = POINTER(vector_info)
        self.spice.ngGet_Vec_Info.argtypes = [c_char_p]
        self.cmd('set nomoremode')

    def vector_names(self, plot=None):
        """
        Names of vectors present in the specified plot
        Names of the voltages, currents, etc present in the specified plot.
        Defaults to the current plot.
        Parameters
        ----------
        plot : str, optional
            Plot name. Defaults to the current plot.
        Returns
        -------
        list of str
            Names of vectors in the plot
        Examples
        --------
        List built-in constants
        >>> ns.vector_names('const')
        ['planck', 'boltz', 'echarge', 'kelvin', 'i', 'c', 'e', 'pi', 'FALSE', 'no', 'TRUE', 'yes']
        Vectors produced by last analysis
        >>> ns.circ('v1 a 0 dc 2');
        >>> ns.operating_point();
        >>> ns.vector_names()
        ['v1#branch', 'a']
        """
        names = []
        if plot is None:
            plot = self.spice.ngSpice_CurPlot().decode('ascii')
        veclist = self.spice.ngSpice_AllVecs(plot.encode('ascii'))
        ii = 0
        while True:
            if not veclist[ii]:
                print(names)
                return names
            names.append(veclist[ii].decode('ascii'))
            ii += 1

    def vectors(self, names=None):
        """
        Dictionary with the specified vectors (defaults to all in current plot)
        Parameters
        ----------
        names : list of str, optional
            Names of vectors to retrieve.  If omitted, return all vectors
            in current plot
        Returns
        -------
        dict from str to ndarray
            Dictionary of vectors.  Keys are vector names and values are Numpy
            arrays containing the data.
        Examples
        --------
        Do an AC sweep and retrieve the frequency axis and output voltage
        >>> nc.ac('dec', 3, 1e3, 10e6);
        >>> nc.ac_results = vectors(['frequency', 'vout'])
        """
        if names is None:
            names = self.vector_names()
        return dict(zip(names, map(self.vector, names)))

    def vector(self, name, plot=None):
        """
        Return a numpy.ndarray with the specified vector
        Uses the current plot by default.
        Parameters
        ----------
        name : str
            Name of vector
        plot : str, optional
            Which plot the vector is in. Defaults to current plot.
        Returns
        -------
        ndarray
            Value of the vector
        Examples
        --------
        Run an analysis and retrieve a vector
        >>> ns.circ(['v1 a 0 dc 2', 'r1 a 0 1k']);
        >>> ns.dc('v1', 0, 2, 1);
        >>> ns.vector('v1#branch')
        array([ 0.   , -0.001, -0.002])
        """
        if plot is not None:
            name = plot + '.' + name
        vec = self.spice.ngGet_Vec_Info(name.encode('ascii'))
        if not vec:
            raise RuntimeError('Vector {} not found'.format(name))
        vec = vec[0]
        if vec.v_length == 0:
            array = np.array([])
        elif vec.v_flags & dvec_flags.vf_real:
            array = np.ctypeslib.as_array(
                vec.v_realdata, shape=(vec.v_length,))
        elif vec.v_flags & dvec_flags.vf_complex:
            components = np.ctypeslib.as_array(vec.v_compdata,
                                               shape=(vec.v_length, 2))
            array = np.ndarray(shape=(vec.v_length,), dtype=np.complex128,
                               buffer=components)
        else:
            raise RuntimeError('No valid data in vector')
        logger.debug('Fetched vector {} type {}'.format(name, vec.v_type))
        array.setflags(write=False)
        if name == 'frequency':
            return array.real
        return array

    def cmd(self, command):
        """
        Send a command to the ngspice engine
        Parameters
        ----------
        command : str
            An ngspice command
        Returns
        -------
        list of str
            Lines of the captured output
        Examples
        --------
        Print all default variables
        >>> ns.cmd('print all')
        ['false = 0.000000e+00',
        'true = 1.000000e+00',
        'boltz = 1.380620e-23',
        'c = 2.997925e+08',
        'e = 2.718282e+00',
        'echarge = 1.602190e-19',
        'i = 0.000000e+00,1.000000e+00',
        'kelvin = -2.73150e+02',
        'no = 0.000000e+00',
        'pi = 3.141593e+00',
        'planck = 6.626200e-34',
        'yes = 1.000000e+00']
        """
        max_length = 1023
        if len(command) > max_length:
            raise ValueError('Command length', len(command), 'greater than',
                             max_length)
        del captured_output[:]
        self.spice.ngSpice_Command(command.encode('ascii'))
        logger.debug('Command %s returned %s', command, captured_output)
        return captured_output

    def circuit(self, netlist):
        netlist_lines = netlist
        if issubclass(type(netlist), str):
            netlist_lines = netlist.split('\n')
        print(len(netlist_lines))
        netlist_lines = [line.encode('ascii') for line in netlist_lines]
        netlist_lines.append(None)
        array = (c_char_p * len(netlist_lines))(*netlist_lines)
        print(len(array))
        return self.spice.ngSpice_Circ(array)

    def transient(self):
        # {} {} {} {}'.format(mode, npoints, fstart, fstop))
        self.cmd('tran 1us 2ms 0')
        return self.vectors()
