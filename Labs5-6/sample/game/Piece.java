package sample.game;

public class Piece {
    public int i;
    public int j;

    public Piece(int i, int j) {
        this.i = i;
        this.j = j;
    }

    public int dist(Piece other){
        return Math.max(Math.abs(this.i - other.i), Math.abs(this.j - other.j));
    }

    public Boolean isValid(){
        return 0 <= i && i <=3 && 0 <= j && j <=3;
    }

    @Override
    public String toString() {
        return "Piece{" +
                "i=" + i +
                ", j=" + j +
                '}';
    }
}
