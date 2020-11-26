import javax.naming.MalformedLinkException;
import java.util.ArrayList;

public class Alphabet_Number_Representation {

    public static void main(String[] args){

        //Test Arguments
        int n = 11;
        String alphabet = "abc";

        //DP Approach

        int a_len = alphabet.length();

        ArrayList<String> solutions = new ArrayList<>();

        for (char c : alphabet.toCharArray()){
            solutions.add(String.valueOf(c));
        }

        for (int i = a_len; i < n; i++){
            solutions.add(solutions.get(Math.floorDiv(i, a_len)) + solutions.get(i%a_len));
        }

        for (int i = 0; i < solutions.size(); i++){
            System.out.print(solutions.get(i) + " ");
        }

    }
}
