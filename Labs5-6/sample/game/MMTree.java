package sample.game;

public class MMTree {
    public MMNode root;
    public boolean alphabeta;
    public Bot myBot;
    public static int MAXX = 10000;

    public MMTree(Board board, Bot bot, boolean alphabeta){
        myBot = bot;
        this.alphabeta = alphabeta;
        this.root = new MMNode();
        root.board = board;
        root.myBot = this.myBot;
        root.depth = 0;
        root.player = '2';
        root.parent = null;
    }

    public Move getBestMove(int depth){
        if (alphabeta){
            int score = root.getScore(depth,-MAXX,MAXX); // in spate construieste arborele cu alpha beta
        }
        else{
            int score = root.getScore(depth); // in spate construieste arborele fara alpha beta
        }
        System.out.println(root.sons.size());
        return root.bestSon.lastMove;
    }
}
