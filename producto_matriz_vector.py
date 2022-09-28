import numpy as np
import ctypes
import time
import statistics
import matplotlib.pyplot as plt

def ctypes_matvecRMRV():
    # ruta de la shared library
    lib = ctypes.CDLL('./ordena_matriz.so')
    
    # tipo de los argumentos
    lib.matvecRMRV.argtypes = [
        np.ctypeslib.ndpointer(dtype=np.double),
        np.ctypeslib.ndpointer(dtype=np.double),
        np.ctypeslib.ndpointer(dtype=np.double),
        ctypes.c_int
    ]
    
    # se devuelve la función configurada
    return lib.matvecRMRV

def ctypes_matvecRMCV():
    # ruta de la shared library
    lib = ctypes.CDLL('./ordena_matriz.so')
    
    # tipo de los argumentos
    lib.matvecRMCV.argtypes = [
        np.ctypeslib.ndpointer(dtype=np.double),
        np.ctypeslib.ndpointer(dtype=np.double),
        np.ctypeslib.ndpointer(dtype=np.double),
        ctypes.c_int
    ]

    # se devuelve la función configurada
    return lib.matvecRMCV

def ctypes_matvecCMRV():
    # ruta de la shared library
    lib = ctypes.CDLL('./ordena_matriz.so')
    
    # tipo de los argumentos
    lib.matvecCMRV.argtypes = [
        np.ctypeslib.ndpointer(dtype=np.double),
        np.ctypeslib.ndpointer(dtype=np.double),
        np.ctypeslib.ndpointer(dtype=np.double),
        ctypes.c_int
    ]
    
    # se devuelve la función configurada
    return lib.matvecCMRV

def ctypes_matvecCMCV():
    # ruta de la shared library
    lib = ctypes.CDLL('./ordena_matriz.so')
    
    # tipo de los argumentos
    lib.matvecCMCV.argtypes = [
        np.ctypeslib.ndpointer(dtype=np.double),
        np.ctypeslib.ndpointer(dtype=np.double),
        np.ctypeslib.ndpointer(dtype=np.double),
        ctypes.c_int
    ]
    
    # se devuelve la función configurada
    return lib.matvecCMCV


if __name__ == '__main__':

    lib = ctypes.CDLL('./ordena_matriz.so')

    #Ruta de la shared library RMRV
    lib.matvecRMRV.argtypes = [
        np.ctypeslib.ndpointer(dtype=np.double),
        np.ctypeslib.ndpointer(dtype=np.double),
        np.ctypeslib.ndpointer(dtype=np.double),
        ctypes.c_int
    ]

    #Ruta de la shared library RMCV
    lib.matvecRMCV.argtypes = [
        np.ctypeslib.ndpointer(dtype=np.double),
        np.ctypeslib.ndpointer(dtype=np.double),
        np.ctypeslib.ndpointer(dtype=np.double),
        ctypes.c_int
    ]

    #Ruta de la shared library CMRV
    lib.matvecCMRV.argtypes = [
        np.ctypeslib.ndpointer(dtype=np.double),
        np.ctypeslib.ndpointer(dtype=np.double),
        np.ctypeslib.ndpointer(dtype=np.double),
        ctypes.c_int
    ]

    #Ruta de la shared library CMCV
    lib.matvecCMCV.argtypes = [
        np.ctypeslib.ndpointer(dtype=np.double),
        np.ctypeslib.ndpointer(dtype=np.double),
        np.ctypeslib.ndpointer(dtype=np.double),
        ctypes.c_int
    ]




    trmrv = []
    trmcv = []
    tcmrv = []
    tcmcv = []
    ns = [16,32,64,128,256,512,1024,2048]
    veces = 5
    for n in ns:
        print(n)
        trmrvi = []
        trmcvi = []
        tcmrvi = []
        tcmcvi = []
        for j in range(veces):
            # datos
            A = np.random.rand(n,n)
            x = np.random.rand(n,1)
            
            # entradas RM
            Arm = A.flatten()
            
            # entradas CM
            Acm = np.transpose(A).flatten()
            
            # referencia
            bref = np.dot(A,x)
            
            # salidas
            bRMRV = np.zeros_like(bref)
            bRMCV = np.zeros_like(bref)
            bCMRV = np.zeros_like(bref)
            bCMCV = np.zeros_like(bref)
            
            # tiempo RMRV
            t = time.time()
            lib.matvecRMRV(Arm,x,bRMRV,n)
            trmrvi.append(time.time() - t)
        
            # tiempo RMCV
            t = time.time()
            lib.matvecRMCV(Arm,x,bRMCV,n)
            trmcvi.append(time.time() - t)
            
            # tiempo CMRV
            t = time.time()
            lib.matvecCMRV(Acm,x,bCMRV,n)
            tcmrvi.append(time.time() - t)
            
            # tiempo CMCV
            t = time.time()
            lib.matvecCMCV(Acm,x,bCMCV,n)
            tcmcvi.append(time.time() - t)
        
        trmrv.append(statistics.median((trmrvi)))
        trmcv.append(statistics.median((trmcvi)))
        tcmrv.append(statistics.median((tcmrvi)))
        tcmcv.append(statistics.median((tcmcvi)))



    #Ahora ploteo los 6 tiempos
    plt.plot(ns,trmrv,'r-',label ="RMRV")
    plt.plot(ns,trmcv,'b-',label = "RMCV")
    plt.plot(ns,tcmrv,'g-',label = "CMRV")
    plt.plot(ns,tcmcv,'y-',label ="CMCV")
    plt.legend(loc = "upper left")
    plt.xlabel("Tamaño")
    plt.ylabel ("Tiempo [us]")
    plt.grid
    plt.savefig("producto_m_v.png",dpi = 500)
    plt.close()

    #SE DETECTA QUE LA MAS LENTA ES RMCV ASI QUE SE USARA PARA EL SPEEDUP
    SUP1 = [i / j for i,j in zip (trmcv, trmrv)]
    SUP2 = [i / j for i,j in zip (trmcv, tcmrv)] 
    SUP3 = [i / j for i,j in zip (trmcv, tcmcv)] 
    plt.plot(ns,SUP1,'g-+')
    plt.plot(ns,SUP2,'y-+')
    plt.plot(ns,SUP3,'r-+')
    plt.xlabel("Tamaño del vector")
    plt.ylabel("Speedup")
    plt.grid
    plt.savefig("speedup-matrizvectorss",dpi=300)
    plt.close()
      



