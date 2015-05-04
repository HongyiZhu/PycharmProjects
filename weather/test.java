import java.io.*;

class test{
	public static void main(String[] args){
		double lat = 32.2217;
		double lon = -110.9264;
		String date = "2015-5-3";
		int hour = 16;
		System.out.println(call_python(lat, lon, date, hour));
	}
	
	public static String call_python(double lat, double lon, String date, int hour){
		String script_path = "C:/Users/zhuhy/script/backend.py";
		Runtime runtime = Runtime.getRuntime();
		String[] cmdarray = {"python", script_path, Double.toString(lat), Double.toString(lon), date, Integer.toString(hour)};
		BufferedReader br = null;
		BufferedReader bre = null;
		try {
			Process process = runtime.exec(cmdarray);
			//read output
			br = new BufferedReader(new InputStreamReader(
					process.getInputStream()));
			StringBuffer linesBuffer = new StringBuffer();
			String line = null;
			while (null != (line = br.readLine())) {
				linesBuffer.append(line).append("\n");
			}
			return linesBuffer.toString();
		} catch (IOException e) {
			e.printStackTrace();
			System.out.println("execute script failed:" + e);
		} finally {
			if (null != br) {
				try {
					br.close();
					br = null;
				} catch (IOException e) {
					e.printStackTrace();
				}
			}
			if (null != bre) {
				try {
					bre.close();
					bre = null;
				} catch (IOException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
			}
		}
		return "";
	}
}