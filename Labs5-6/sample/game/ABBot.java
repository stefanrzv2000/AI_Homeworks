package sample.game;

public class ABBot extends Bot {

    private int maxDepth;

    public ABBot(Board board, int maxDepth) {
        super(board);
        type = "alphabeta";
        this.maxDepth = maxDepth;
    }

    @Override
    public Move getNextMove() {
        MMTree tree = new MMTree(trueBoard, this, true);
        return tree.getBestMove(maxDepth);
    }
}
