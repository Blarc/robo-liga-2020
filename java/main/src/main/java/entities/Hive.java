package entities;

import com.fasterxml.jackson.annotation.JsonProperty;
import enums.HiveType;

import java.util.Map;

public class Hive extends MovableObject {
    @JsonProperty("type")
    private HiveType type;
    private Integer teamOneWorth;
    private Integer teamTwoWorth;

    public Hive(Integer id, Integer direction, Point position, HiveType type, Integer teamOneWorth, Integer teamTwoWorth) {
        super(id, direction, position);
        this.type = type;
        this.teamOneWorth = teamOneWorth;
        this.teamTwoWorth = teamTwoWorth;
    }

    @JsonProperty("points")
    private void parseWorths(Map<String, Object> points) {
        teamOneWorth = ((Integer) points.get("team1"));
        teamOneWorth = ((Integer) points.get("team2"));
    }

    public HiveType getType() {
        return type;
    }

    public Integer getTeamOneWorth() {
        return teamOneWorth;
    }

    public Integer getTeamTwoWorth() {
        return teamTwoWorth;
    }
}
