import numpy as np
import ctypes
import time
import statistics
import math
import matplotlib.pyplot as plt

if __name__ == '__main__':

    lib = ctypes.CDLL('./unrolling_test.so')
    lib.funcion_sin_unrolling.argtypes = [np.ctypeslib.ndpointer(dtype=np.int32),np.ctypeslib.ndpointer(dtype=np.int32),ctypes.c_int]
    lib.funcion_con_unrolling.argtypes = [np.ctypeslib.ndpointer(dtype=np.int32),np.ctypeslib.ndpointer(dtype=np.int32),ctypes.c_int]


    with_unrolling_master = []
    without_unrolling_master = []

    tamanos = [128,256,512,1024,2048]
    iteraciones = 5

    for n in tamanos:

        lista_with = []
        lista_without = []

        for it in range(iteraciones):

            #UNROLLING ACTIVADO
            
            a = np.random.randint(5,size = n, dtype=np.int32)
            b = np.random.randint(5, size = n, dtype=np.int32)

            #Como c es una constante arbitaria decidimos ponerle el valor de la iteracion actual
      

            tic1 = time.time()
            lib.funcion_sin_unrolling(a,b,it)
            toc1 = time.time()

            lista_with.append(1e6*(toc1-tic1))

            #SIN UNROLLING 

            a = np.random.randint(5,size = n, dtype = np.int32)
            b = np.random.randint(5, size = n, dtype = np.int32)

            tic2 = time.time()
            lib.funcion_con_unrolling(a,b,it)
            toc2 = time.time()

            lista_without.append(1e6*(toc2-tic2))
        
        with_unrolling_master.append(statistics.median(lista_with))
        without_unrolling_master.append(statistics.median(lista_without))
    
    plt.plot(tamanos,lista_with,'r-')
    plt.plot(tamanos,lista_without,'b-')
    plt.xlabel("Size")
    plt.ylabel ("Tiempo [us]")
    plt.grid
    plt.savefig("unrolling.png",dpi = 300)
    plt.close()


    #notamos que para tamaños pequeños el unrolling hace la ejecucion más lenta; sin embargo, para arreglos largos 
    #el unrolling ayuda a conseguir una ejecución más rapida

    SUP1 = [i / j for i,j in zip (with_unrolling_master, without_unrolling_master)] 
    plt.plot(tamanos,SUP1,'g-+')
    plt.xlabel("Tamaño del vector")
    plt.ylabel("Tiempo [us]")
    plt.grid
    plt.savefig("speedup-unrolling",dpi=300)
    plt.close()    



    




