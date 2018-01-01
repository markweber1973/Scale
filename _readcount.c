#include <Python.h>
#include "readcount.h"


static char module_docstring[] =
    "This module provides an interface for reading the scale count using C.";
static char readcount_docstring[] =
    "readcount docvalue.";

static PyObject *readcount_readcount(PyObject *self, PyObject *args);

static PyMethodDef module_methods[] = {
    {"readcount", readcount_readcount, METH_VARARGS, readcount_docstring},
    {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC init_readcount(void)
{
    PyObject *m = Py_InitModule3("_readcount", module_methods, module_docstring);
    if (m == NULL)
        return;
}

static PyObject *readcount_readcount(PyObject *self, PyObject *args)
{
    unsigned long value = readcount();
    PyObject *ret = Py_BuildValue("k", value);
    return ret;
}

