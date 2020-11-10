package sample.game;

public class Board {

    public static int HUMAN = 1;
    public static int BOT = 2;

    char[][] matrix = new char[4][4];
    public int currentPlayer;

    public Bot bot;

    public Board(){}

    public Board(String botType, int maxDepth){
        for (int i = 0; i < 4; i++){
            matrix[0][i] = '2';
            matrix[1][i] = ' ';
            matrix[2][i] = ' ';
            matrix[3][i] = '1';
        }
        bot = Bot.getBot(botType,this,maxDepth);
        currentPlayer = HUMAN;
    }

    public char getPiece(int i, int j){
        return matrix[i][j];
    }

    public char getPiece(Piece p){
        return matrix[p.i][p.j];
    }

    public Board movePiece(Piece p1, Piece p2){
        if(!canMovePiece(p1,p2)) return this;

        matrix[p2.i][p2.j] = matrix[p1.i][p1.j];
        matrix[p1.i][p1.j] = ' ';
        return this;
    }

    public Board movePiece(Move move){
        return movePiece(move.from,move.to);
    }

    public Boolean canMovePiece(Piece p1, Piece p2){
        if (getPiece(p1) == ' '){
            return false;
        }

        if (getPiece(p2) != ' '){
            return false;
        }

        if (p1.dist(p2) != 1){
            return false;
        }

        return true;
    }

    public Boolean canMovePiece(Move move){
        return canMovePiece(move.from, move.to);
    }

    private Boolean isFirstWinner(){

        for(int i = 0; i < 4; i++){
            if (matrix[0][i] != '1'){
                return false;
            }
        }
        return true;
    }

    private Boolean isSecondWinner(){

        for(int i = 0; i < 4; i++){
            if (matrix[3][i] != '2'){
                return false;
            }
        }
        return true;
    }

    public int getWinner(){
        if (isFirstWinner()) return 1;
        if (isSecondWinner()) return 2;
        return 0;
    }

    public Board copy(){
        var bc = new Board();
        for(int i = 0; i < 4; i++){
            for (int j = 0; j < 4; j++){
                bc.matrix[i][j] = this.matrix[i][j];
            }
        }
        bc.currentPlayer = currentPlayer;
        bc.bot = bot;
        return bc;
    }

    public void makeBotMove(){
        Move move = bot.getNextMove();
        movePiece(move);
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < 4; i++){
            for (int j = 0; j < 4; j++){
                sb.append(matrix[i][j]).append(" ");
            }
            sb.append("\n");
        }
        return sb.toString();
    }
}
