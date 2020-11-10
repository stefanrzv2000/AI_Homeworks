package sample;

import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.control.Alert;
import javafx.scene.input.MouseEvent;
import javafx.scene.layout.*;
import javafx.scene.paint.Color;
import sample.game.Board;
import sample.game.Piece;

import java.net.URL;
import java.util.ResourceBundle;

public class Controller implements Initializable {

    @FXML
    Pane MainPane, canvasPane;
    @FXML
    Canvas gameCanvas;

    private Board board = new Board("smart",4);
    private GraphicsContext gc;
    private Piece selectedPiece = null;
    Color col_b1 = Color.CORAL, col_b2 = Color.WHEAT;
    Color col_p1 = Color.BLUEVIOLET, col_p2 = Color.SEAGREEN;

    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {
        gc = gameCanvas.getGraphicsContext2D();
        drawBoard(col_b1,col_b2);
        drawPieces(col_p1,col_p2);
    }

    private void drawBoard(Color c1, Color c2){

        var h = gameCanvas.getHeight();
        var w = gameCanvas.getWidth();

        gc.setFill(c1);
        //gc.fillRect(0,0,h/size,w/size);
        for (int i = 0; i < 4; i++){
            for (int j = 0; j < 4; j++){
                if ( (i+j) % 2 == 1) {
                    gc.setFill(c1);
                } else {
                    gc.setFill(c2);
                }
                gc.fillRect(i*w/4,j*w/4,h/4,w/4);
            }
        }
    }

    private void drawPieces(Color c1, Color c2){

        var h = gameCanvas.getHeight();
        var w = gameCanvas.getWidth();
        var diameter = Math.min(h,w)/6;

        for(int i = 0; i < 4; i++){
            for (int j = 0; j < 4; j++){
                if (board.getPiece(i,j) == '1'){
                    gc.setFill(c1);
                    gc.fillOval((6*j+1)*h/24,(6*i+1)*w/24,diameter,diameter);
                }
                if (board.getPiece(i,j) == '2'){
                    gc.setFill(c2);
                    gc.fillOval((6*j+1)*h/24,(6*i+1)*w/24,diameter,diameter);
                }
            }
        }
    }

    public void onCanvasClicked(MouseEvent e){

        if(board.currentPlayer != Board.HUMAN){
            return;
        }

        var x = e.getX();
        var y = e.getY();

        var h = gameCanvas.getHeight();
        var w = gameCanvas.getWidth();
        var diameter = Math.min(h,w)/6;

        var j = (int) (4*x/w);
        var i = (int) (4*y/h);

        if(selectedPiece == null){
            System.out.println("Selected Piece is NULL");
            if(board.getPiece(i,j) == '1'){
                selectedPiece = new Piece(i,j);
                gc.setStroke(Color.RED);
                gc.setLineWidth(3);
                gc.strokeOval((6*j+1)*h/24,(6*i+1)*w/24,diameter,diameter);
            }
        }
        else{
            System.out.println("Selected Piece: " + selectedPiece.i + " " + selectedPiece.j);
            var newPiece = new Piece(i,j);
            System.out.println("New Piece: " + newPiece.i + " " + newPiece.j);
            if(board.canMovePiece(selectedPiece,newPiece)){
                board.movePiece(selectedPiece,newPiece);

                drawBoard(col_b1,col_b2);
                drawPieces(col_p1,col_p2);
                if(board.getWinner() == 1){
                    announceWin();
                }

                board.makeBotMove();
                drawBoard(col_b1,col_b2);
                drawPieces(col_p1,col_p2);

                if(board.getWinner() == 2){
                    announceLose();
                }
            }
            drawBoard(col_b1,col_b2);
            drawPieces(col_p1,col_p2);
            selectedPiece = null;
            System.out.println(board);

        }
    }

    void announceWin(){
        Alert alert = new Alert(Alert.AlertType.INFORMATION);
        alert.setTitle("Congrats!");
        alert.setHeaderText(null);
        alert.setContentText("You WON!");

        alert.showAndWait();
        System.exit(0);
    }

    void announceLose(){
        Alert alert = new Alert(Alert.AlertType.INFORMATION);
        alert.setTitle("Looser!");
        alert.setHeaderText(null);
        alert.setContentText("You LOST!");

        alert.showAndWait();
        System.exit(0);
    }
}
