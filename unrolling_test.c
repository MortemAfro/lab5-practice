void funcion_sin_unrolling(int *a, int *b, int c){
    for(int i=0;i<30;i++){
        a[i] = a[i] + b[i]*c;
    }
}

void funcion_con_unrolling(int *a, int *b, int c){
    for(int i=0;i<30;i+=3){
        a[i] = a[i] + b[i]*c;
        a[i+1] = a[i+1] + b[i+1]*c;
        a[i+2] = a[i+2] + b[i+2]*c;
    }
}