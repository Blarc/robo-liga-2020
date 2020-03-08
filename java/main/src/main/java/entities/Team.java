package entities;

import com.fasterxml.jackson.annotation.JsonProperty;

public class Team {
    @JsonProperty("id")
    private Integer id;
    @JsonProperty("name")
    private String name;
    @JsonProperty("score")
    private Integer score;

    public Integer getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public Integer getScore() {
        return score;
    }
}
