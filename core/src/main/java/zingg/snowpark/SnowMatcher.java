package zingg.snowpark;

import java.util.ArrayList;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import com.snowflake.snowpark_java.Column;
import com.snowflake.snowpark_java.DataFrame;
import com.snowflake.snowpark_java.Row;
import com.snowflake.snowpark_java.Functions;
// import com.snowflake.snowpark_java.catalyst.encoders.RowEncoder;
// import com.snowflake.snowpark_java.expressions.Window;
// import com.snowflake.snowpark_java.expressions.WindowSpec;
import com.snowflake.snowpark_java.types.DataType;
import com.snowflake.snowpark_java.Session;

import scala.collection.JavaConverters;
import zingg.Matcher;
import zingg.block.Block;
import zingg.block.Canopy;
import zingg.block.Tree;
import zingg.model.Model;
import zingg.snowpark.model.SnowModel;
import zingg.client.Arguments;
import zingg.client.SparkFrame;
import zingg.client.ZFrame;
import zingg.client.ZinggClientException;
import zingg.client.ZinggOptions;
import zingg.util.Analytics;
import zingg.util.BlockingTreeUtil;
import zingg.client.util.ColName;
import zingg.client.util.ColValues;
import zingg.util.Metric;
import zingg.client.util.Util;
import zingg.util.DSUtil;
import zingg.util.GraphUtil;
import zingg.util.HashUtil;
import zingg.util.ModelUtil;
import zingg.util.PipeUtilBase;

public class SnowMatcher extends Matcher<Session,DataFrame,Row,Column,DataType>{


	public static String name = "zingg.Matcher";
	public static final Log LOG = LogFactory.getLog(SnowMatcher.class);    

	

	@Override
	public void cleanup() throws ZinggClientException {
		// TODO Auto-generated method stub
		
	}

	

	@Override
	protected Model getModel() {
		Model model = new SnowModel(this.featurers);
		model.register(getContext());
		model.load(args.getModel());
		return model;
	}



	@Override
	public void setSession(Session session) {
		// TODO Auto-generated method stub
		
	}

}
