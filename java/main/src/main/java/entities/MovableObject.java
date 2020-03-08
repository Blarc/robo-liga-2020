package entities;

import com.fasterxml.jackson.annotation.JsonProperty;

public class MovableObject {
    @JsonProperty("id")
    private Integer id;
    @JsonProperty("dir")
    private Integer direction;
    @JsonProperty("position")
    private Point position;

    public MovableObject(Integer id, Integer direction, Point position) {
        this.id = id;
        this.direction = direction;
        this.position = position;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public Integer getDirection() {
        return direction;
    }

    public void setDirection(Integer direction) {
        this.direction = direction;
    }

    public Point getPosition() {
        return position;
    }

    public void setPosition(Point position) {
        this.position = position;
    }
}
