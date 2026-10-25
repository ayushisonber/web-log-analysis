import java.io.IOException;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class PageMapper
        extends Mapper<Object, Text, Text, Text> {

    private Text page = new Text();
    private Text result = new Text();

    public void map(Object key, Text value, Context context)
            throws IOException, InterruptedException {

        String line = value.toString();

        String[] parts = line.split("\\s+");

        if (parts.length == 3) {

            String userId = parts[0];
            String pageName = parts[1];
            int timeSpent = Integer.parseInt(parts[2]);

            page.set(pageName);

            result.set("1," + timeSpent);

            context.write(page, result);
        }
    }
}
