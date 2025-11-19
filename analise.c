/* analise.c */

/*
   Esta função será o nosso "módulo crítico".
   Ela será "exportada" para que o Python (app.py) a possa encontrar.
   
   __declspec(dllexport) é a magia que diz ao compilador para 
   tornar esta função visível dentro do ficheiro .dll.
*/

__declspec(dllexport)
int verificar_risco_ia(double media_notas, int total_faltas) {
    
    // As mesmas regras que tínhamos no app.py
    double LIMITE_MEDIA_NOTAS = 6.0;
    int LIMITE_FALTAS = 3;

    int risco_media = 0;
    int risco_faltas = 0;

    // 1. Verifica a média
    if (media_notas < LIMITE_MEDIA_NOTAS) {
        risco_media = 1; // 1 = Risco de Média
    }

    // 2. Verifica as faltas
    if (total_faltas > LIMITE_FALTAS) {
        risco_faltas = 2; // 2 = Risco de Faltas
    }

    /* Retorna um código de status combinado:
       0 = OK (Sem risco)
       1 = Risco de Média Baixa
       2 = Risco de Muitas Faltas
       3 = Risco de Média E Faltas (1 + 2)
    */
    return risco_media + risco_faltas;
}