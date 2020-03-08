package entities;

import com.fasterxml.jackson.annotation.JsonProperty;

public class Field {
    @JsonProperty("bottomLeft")
    private Point bottomLeft;
    @JsonProperty("bottomRight")
    private Point bottomRight;
    @JsonProperty("topLeft")
    private Point topLeft;
    @JsonProperty("topRight")
    private Point topRight;

    public Field(Point bottomLeft, Point bottomRight, Point topLeft, Point topRight) {
        this.bottomLeft = bottomLeft;
        this.bottomRight = bottomRight;
        this.topLeft = topLeft;
        this.topRight = topRight;
    }

    public Point getBottomLeft() {
        return bottomLeft;
    }

    public void setBottomLeft(Point bottomLeft) {
        this.bottomLeft = bottomLeft;
    }

    public Point getBottomRight() {
        return bottomRight;
    }

    public void setBottomRight(Point bottomRight) {
        this.bottomRight = bottomRight;
    }

    public Point getTopLeft() {
        return topLeft;
    }

    public void setTopLeft(Point topLeft) {
        this.topLeft = topLeft;
    }

    public Point getTopRight() {
        return topRight;
    }

    public void setTopRight(Point topRight) {
        this.topRight = topRight;
    }
}
