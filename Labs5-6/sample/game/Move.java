package sample.game;

public class Move {
    Piece from;
    Piece to;

    public Move(Piece from, Piece to){
        this.from = from;
        this.to = to;
    }

    @Override
    public String toString() {
        return "Move{" +
                "from=" + from +
                ", to=" + to +
                '}';
    }
}
