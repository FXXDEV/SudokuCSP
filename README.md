# Sudoku com CSP 

## Objetivo do Jogo

* Preencher todos os valores tabela 9x9

## Regras 
 As regras do sudoku (que em japonês significa "número único) são simples e, apesar de apresentar números, não é necessário fazer qualquer tipo de conta. Basta completar todos os espaços seguindo as seguintes restrições:

    * Não repetir números na mesma linha, na mesma coluna nem na mesma grade 3x3.
    * Cada linha, coluna ou grade possuem números de 1 a 9.

## CSP

Para este projeto foi utilizado busca reversa(backtracking) e consistencia local (AC-3)

#### Variáveis
 * Combinação de letra indicando a linha e digito indicando coluna.  X = {X<sub>1</sub>, X<sub>2</sub>, ..., X<sub>81</sub>}

#### Domínio
 * Cada variável Xi possui digitos de 1 a 9 
 * D = {D<sub>1</sub>, D<sub>2</sub>, ..., D<sub>81</sub>}
 * D<sub>i</sub> = {1, 2, 3, 4, 5, 6, 7, 8, 9}

#### Restrições
* O valor da variável X<sub>i</sub> não pode ser igual a nenhum valor presente nas linhas, colunas, e grades.



* Para executar, basta rodar python sudoku.py start_sudoku/dificuldade_escolhida.txt *