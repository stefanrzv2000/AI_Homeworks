package sample.game;

import java.util.ArrayList;
import java.util.List;

public abstract class Bot {
    protected Board trueBoard;
    public String type;

    public Bot(Board board){
        this.trueBoard = board;
    }

    public static Bot getBot(String type, Board board, int maxDepth){
        switch (type.toLowerCase()){
            case "naive":
                return new NaiveBot(board);
            case "counter":
                return new CounterBot(board);
            case "minimax":
                return new MinimaxBot(board,maxDepth);
            case "alphabeta":
                return new ABBot(board,maxDepth);
            case "smart":
                return new SmartBot(board,maxDepth);
        }
        return null;
    }

    public abstract Move getNextMove();

    public int evaluate(Board board) {
        int score = 12;
        for (int i = 0; i < 4; i++){
            for (int j = 0; j < 4; j++){
                if(board.getPiece(i,j) != ' '){
                    score -= (3-i);
                }
            }
        }
        return score;
    }

    public int evaluate(Board board, Move move){
        return evaluate(board.copy().movePiece(move));
    }

    public int evaluate(Move move){
        return evaluate(trueBoard,move);
    }

    private int[] xs = {1,0,-1,0,1,1,-1,-1};
    private int[] ys = {0,1,0,-1,1,-1,1,-1};

    public List<Move> getMoves(Board board){
        var moves = new ArrayList<Move>();
        for(int i = 0; i < 4; i++){
            for(int j = 0; j < 4; j++){
                if(board.getPiece(i,j) == '2'){
                    var mine = new Piece(i,j);
                    for (int k = 0; k < 8; k++){
                        var next = new Piece(i+xs[k],j+ys[k]);
                        if(next.isValid() && board.getPiece(next) == ' '){
                            moves.add(new Move(mine,next));
                        }
                    }
                }
            }
        }

        return moves;
    }
}
