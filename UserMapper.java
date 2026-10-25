import java.io.IOException;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;

import org.apache.hadoop.mapreduce.Mapper;

public class UserMapper
        extends Mapper<Object, Text, Text, IntWritable> {

    private Text user = new Text();
    private IntWritable time = new IntWritable();

    public void map(Object key, Text value, Context context)
            throws IOException, InterruptedException {

        String line = value.toString();

        String[] parts = line.split("\\s+");

        if (parts.length == 3) {

            String userId = parts[0];

            int timeSpent =
                    Integer.parseInt(parts[2]);

            user.set(userId);

            time.set(timeSpent);

            context.write(user, time);
        }
    }
}
