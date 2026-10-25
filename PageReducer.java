import java.io.IOException;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

public class PageReducer
        extends Reducer<Text, Text, Text, Text> {

    private Text result = new Text();

    public void reduce(Text key, Iterable<Text> values,
                        Context context)
            throws IOException, InterruptedException {

        int totalVisits = 0;
        int totalTime = 0;

        for (Text value : values) {

            String[] parts = value.toString().split(",");

            int visits = Integer.parseInt(parts[0]);
            int time = Integer.parseInt(parts[1]);

            totalVisits += visits;
            totalTime += time;
        }

        result.set("Visits = " + totalVisits +
                   " TimeSpent = " + totalTime);

        context.write(key, result);
    }
}
