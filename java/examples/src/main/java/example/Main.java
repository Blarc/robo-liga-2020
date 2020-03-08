package example;

import ev3dev.utils.Interpolation;

public class Main {
    public static void main(String[] args) {

        float data = Interpolation.interpolate(15, 10, 20, 10, 20);

        System.out.println(data);

    }

}
