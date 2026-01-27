fn main() {
    mut x := 10;
    mut y := 5;
    mut resultado := 0;

    // Expressões aritméticas
    resultado = x + y * 2;
    resultado = (x + y) * 2;

    // Expressões relacionais e lógicas
    if x > y && resultado >= 20 {
        resultado = resultado + 1;
    } else {
        resultado = resultado - 1;
    }

    // Laço de repetição
    for x < 15 {
        x = x + 1;
        resultado = resultado + x;
    }

    // Uso de booleanos
    if true || false {
        resultado = resultado + 10;
    }

    // String literal (não usada semanticamente ainda, mas testada)
    mut mensagem := "Resultado final";

    return resultado;
}
