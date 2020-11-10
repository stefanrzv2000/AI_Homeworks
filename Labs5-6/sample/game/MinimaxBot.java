package sample.game;

public class MinimaxBot extends Bot {

    private int maxDepth;

    public MinimaxBot(Board board, int maxDepth) {
        super(board);
        type = "minimax";
        this.maxDepth = maxDepth;

    }

    @Override
    public Move getNextMove() {
        MMTree tree = new MMTree(trueBoard,this,false);
        return tree.getBestMove(maxDepth);
    }
}

