## English

# GoGetYourPDF

GoGetYourPDF is a Python script that generates a PDF document from a Go game record in SGF format. Each turn in the game is represented as a page in the PDF, with a high-resolution image of the board state. Any comments associated with a turn are also included on the same page.

## How to Use

1. Ensure that you have Python installed, along with the required libraries: `argparse`, `re`, `matplotlib`, `fpdf`, and `numpy`.

2. Save your Go game record in SGF format.

3. Run the script from the command line using the `-i` option to specify the input SGF file and the `-o` option to specify the output PDF file. For example:

```bash
python go_get_your_pdf.py -i game1.sgf -o go_game_with_high_res_images.pdf
```

Please note that this script currently does not support the Go capture rule. This will cause captured pieces to remain on the board unless they are replaced by others afterwards.

## Português

# GoGetYourPDF

GoGetYourPDF é um script Python que gera um documento PDF a partir de um registro de jogo de Go no formato SGF. Cada turno no jogo é representado como uma página no PDF, com uma imagem de alta resolução do estado do tabuleiro. Quaisquer comentários associados a um turno também são incluídos na mesma página.

## Como usar

1. Certifique-se de que você tenha o Python instalado, juntamente com as bibliotecas necessárias: `argparse`, `re`, `matplotlib`, `fpdf` e `numpy`.

2. Salve o registro do seu jogo de Go no formato SGF.

3. Execute o script a partir da linha de comando usando a opção `-i` para especificar o arquivo SGF de entrada e a opção `-o` para especificar o arquivo PDF de saída. Por exemplo:

```bash
python go_get_your_pdf.py -i game1.sgf -o go_game_with_high_res_images.pdf
```

Por favor, note que este script atualmente não suporta a regra de captura de Go. Isso fará com que peças capturadas permaneçam no tabuleiro a não ser que sejam substituídas por outras em seguida.
