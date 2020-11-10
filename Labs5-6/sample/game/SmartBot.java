package sample.game;

public class SmartBot extends Bot {

    private int maxDepth;

    public SmartBot(Board board, int maxDepth) {
        super(board);
        type = "alphabeta";
        this.maxDepth = maxDepth;
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


        for (int i = 0; i < 4; i++){
            for (int j = 0; j < 4; j++){
                if(board.getPiece(i,j) != '1'){
                    if(i > 0){
                        boolean canMoveForward = false;
                        for (int k = 0; k < 3; k++){
                            int index = j-i+k;
                            if(index >= 0 && index <= 3 && board.getPiece(i,index) == ' '){
                                canMoveForward = true;
                                break;
                            }
                        }
                        if(!canMoveForward){
                            score += 1;
                        }
                    }
                }
            }
        }

        return score;
    }

    @Override
    public Move getNextMove() {
        MMTree tree = new MMTree(trueBoard, this, true);
        return tree.getBestMove(maxDepth);
    }
}