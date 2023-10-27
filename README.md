# daily_fifa

Projeto utilizando AWS Lambda, AWS DynamoDB e AWS API Gateway\n
para criação de um microsserviço para adicionar resultados de jogos,\n
através de uma interface Tkinter, em uma tabela de banco de dados.

O projeto consiste em, por enquanto, 3 api's GET, onde é criado um resumo\n
com GET's de:\n
- Timestamp\n
- Competição\n
- Semana\n

E os resultados são postados utilizando uma requisição POST.\n

Para a interface grafica, foi criado uma janela com a Biblioteca\n
Python Tkinter, e lá são passados os parametros necessarios para\n
o preenchimento dos dados.
