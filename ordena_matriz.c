//file matvecRMRV.c
void matvecRMRV(double *A, double *x, double *b, int N)
{
    float tmp = 0.0;
    for(int i = 0; i < N; i++)
    {
        tmp = 0.0;
        for(int j = 0; j < N; j++)
        {
            tmp += A[i*N + j]*x[j];
        }
        b[i] = tmp;
    }
}

//file matvecRMCV.c
void matvecRMCV(double *A, double *x, double *b, int N)
{
    float tmp = 0.0;
    for(int j = 0; j < N; j++)
    {
        for(int i = 0; i < N; i++)
        {
            b[i] += A[i*N + j]*x[j];
        }
    }
}

//file matvecCMRV.c
void matvecCMRV(double *A, double *x, double *b, int N)
{
    float tmp = 0.0;
    for(int i = 0; i < N; i++)
    {
        tmp = 0.0;
        for(int j = 0; j < N; j++)
        {
            tmp += A[i + j*N]*x[j];
        }
        b[i] = tmp;
    }
}

//file matvecCMCV.c
void matvecCMCV(double *A, double *x, double *b, int N)
{
    for(int j = 0; j < N; j++)
    {
        for(int i = 0; i < N; i++)
        {
            b[i] += A[i + j*N]*x[j];
        }
    }
}