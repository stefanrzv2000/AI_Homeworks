package sample.game;

import java.util.Comparator;

public class NaiveBot extends Bot {
    public NaiveBot(Board board) {
        super(board);
        type = "naive";
    }

    @Override
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

    @Override
    public Move getNextMove() {
        try {
            Thread.sleep(5);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        var possibleMoves = getMoves(trueBoard);
        System.out.println(possibleMoves);
        var nb = this;
        possibleMoves.sort(Comparator.comparingInt(nb::evaluate));
        return possibleMoves.get(possibleMoves.size()-1);
    }
}
