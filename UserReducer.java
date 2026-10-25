import java.io.IOException;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;

import org.apache.hadoop.mapreduce.Reducer;

public class UserReducer
        extends Reducer<Text, IntWritable,
                         Text, IntWritable> {

    private IntWritable result =
            new IntWritable();

    public void reduce(Text key,
                        Iterable<IntWritable> values,
                        Context context)
            throws IOException, InterruptedException {

        int totalTime = 0;

        for (IntWritable value : values) {

            totalTime += value.get();
        }

        result.set(totalTime);

        context.write(key, result);
    }
}

