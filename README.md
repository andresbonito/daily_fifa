# daily_fifa

Projeto utilizando AWS Lambda, AWS DynamoDB e AWS API Gateway<br>
para criação de um microsserviço para adicionar resultados de jogos,<br>
através de uma interface Tkinter, em uma tabela de banco de dados.

O projeto consiste em, por enquanto, 3 api's GET, onde é criado um resumo<br>
com GET's de:<br>
- Timestamp<br>
- Competição<br>
- Semana<br>

E os resultados são postados utilizando uma requisição POST.<br>

Para a interface grafica, foi criado uma janela com a Biblioteca<br>
Python Tkinter, e lá são passados os parametros necessarios para<br>
o preenchimento dos dados.
