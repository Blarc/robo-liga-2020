package entities;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.core.JsonFactory;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import enums.HiveType;

import java.util.HashSet;
import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;

public class GameData {
    private Field teamOneBasket;
    private Field teamTwoBasket;
    private Field field;
    private Field neutralZone;
    private Field teamOneZone;
    private Field teamTwoZone;

    private HashSet<Hive> healthyHives;
    private HashSet<Hive> diseasedHives;

    private Set<MovableObject> robots;

    private Team teamOne;
    private Team teamTwo;

    @JsonProperty("gameOn")
    private Boolean gameOn;

    @JsonProperty("timeLeft")
    private Integer timeLeft;

    @SuppressWarnings("unchecked")
    @JsonProperty("fields")
    private void parseFields(Map<String, Object> fields) {
        Map<String, Object> baskets = ((Map<String, Object>) fields.get("baskets"));
        Map<String, Object> zones = ((Map<String, Object>) fields.get("zones"));

        new ObjectMapper().readerFor(Field.class);
        field = ((Field) fields.get("field"));
        teamOneBasket = ((Field) baskets.get("team1"));
        teamTwoBasket = ((Field) baskets.get("team2"));
        neutralZone = ((Field) zones.get("neutral"));
        teamOneZone = ((Field) zones.get("team1"));
        teamTwoZone = ((Field) zones.get("team2"));
    }

    @SuppressWarnings("unchecked")
    @JsonProperty("objects")
    private void parseObjects(Map<String, Object> objects) {
        healthyHives = new HashSet<>();
        diseasedHives = new HashSet<>();
        ((Map<String, Object>) objects.get("hives")).values().stream()
                .map(o -> ((Hive) o))
                .forEach(hive -> {
                    if (hive.getType() == HiveType.HIVE_HEALTHY) {
                        healthyHives.add(hive);
                    }
                    else {
                        diseasedHives.add(hive);
                    }
                });

        robots = ((Map<String, Object>) objects.get("robots")).values().stream()
                .map(o -> ((MovableObject) o))
                .collect(Collectors.toSet());
    }

    @JsonProperty("teams")
    private void parseTeams(Map<String, Object> teams) {
        teamOne = ((Team) teams.get("team1"));
        teamTwo = ((Team) teams.get("team2"));
    }


    public Field getTeamOneBasket() {
        return teamOneBasket;
    }

    public Field getTeamTwoBasket() {
        return teamTwoBasket;
    }

    public Field getField() {
        return field;
    }

    public Field getNeutralZone() {
        return neutralZone;
    }

    public Field getTeamOneZone() {
        return teamOneZone;
    }

    public Field getTeamTwoZone() {
        return teamTwoZone;
    }

    public HashSet<Hive> getHealthyHives() {
        return healthyHives;
    }

    public HashSet<Hive> getDiseasedHives() {
        return diseasedHives;
    }

    public Set<MovableObject> getRobots() {
        return robots;
    }

    public Team getTeamOne() {
        return teamOne;
    }

    public Team getTeamTwo() {
        return teamTwo;
    }

    public Integer getTimeLeft() {
        return timeLeft;
    }

    public Boolean getGameOn() {
        return gameOn;
    }
}
