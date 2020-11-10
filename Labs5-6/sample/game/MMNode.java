package sample.game;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;

public class MMNode {
    public Board board;
    public char player;
    public Integer score = null;
    public int depth;
    public Bot myBot;
    public Move lastMove;

    List<MMNode> sons = new ArrayList<>();
    MMNode bestSon = null;
    MMNode parent;

    public void generateSons(){
        var moves = getMoves(board,player);
        for (var m: moves){
            var bc = board.copy();
            bc.movePiece(m);

            var son = new MMNode();
            son.board = bc;
            son.player = (char) ('0' + '3' - player);
            son.depth = depth + 1;
            son.myBot = myBot;
            son.parent = this;
            son.lastMove = m;
            sons.add(son);
        }
    }

    public int getScore(int maxDepth){
        if (score!=null){
            return score;
        }

        //verificam daca e endgame
        var win = board.getWinner();
        if(win == 1){
            score = -100;
            return score;
        }
        if(win == 2){
            score = 100;
            return score;
        }

        // verificam daca am ajuns la max depth
        if (depth == maxDepth){
            score = myBot.evaluate(board);
            return score;
        }

        // verificam daca am evaluat deja toti fiii
        if (bestSon != null){
            score = bestSon.score;
            return score;
        }

        // generam toti fiii daca e nevoie
        if (sons.size() == 0){
            generateSons();
        }
        if (player == '1'){
            bestSon = Collections.min(sons,Comparator.comparingInt(o->o.getScore(maxDepth)));
        }
        else{
            bestSon = Collections.max(sons,Comparator.comparingInt(o->o.getScore(maxDepth)));
        }

        score = bestSon.score;
        return score;
    }

    public int getScore(int maxDepth, int alpha, int beta){
        if (score!=null){
            return score;
        }

        //verificam daca e endgame
        var win = board.getWinner();
        if(win == 1){
            score = -100;
            return score;
        }
        if(win == 2){
            score = 100;
            return score;
        }

        // verificam daca am ajuns la max depth
        if (depth == maxDepth){
            score = myBot.evaluate(board);
            return score;
        }

        // generam toti fiii daca e nevoie
        if (sons.size() == 0){
            generateSons();
        }
        if (player == '1'){ // cautam minim
            score = 1000;

            for (var s: sons){
                int son_score = s.getScore(maxDepth,alpha,beta);
                if (score > son_score){
                    score = son_score;
                    bestSon = s;
                }
                beta = Math.min(beta,score);
                if (alpha>=beta) break;
            }
        }
        else{ // player = 2, cautam maxim
            score = -1000;

            for (var s: sons){
                int son_score = s.getScore(maxDepth,alpha,beta);
                if (score < son_score){
                    score = son_score;
                    bestSon = s;
                }
                alpha = Math.max(alpha,score);
                if (alpha>=beta) break;
            }
        }

        return score;
    }

    private int[] xs = {1,0,-1,0,1,1,-1,-1};
    private int[] ys = {0,1,0,-1,1,-1,1,-1};

    public List<Move> getMoves(Board board, char player){
        var moves = new ArrayList<Move>();
        for(int i = 0; i < 4; i++){
            for(int j = 0; j < 4; j++){
                if(board.getPiece(i,j) == player){
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
