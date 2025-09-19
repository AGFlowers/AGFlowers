import java.io.File;
import java.lang.management.ManagementFactory;
import java.lang.management.OperatingSystemMXBean;

public class SystemHealthCheck {
    public static void main(String[] args) {
        // OS Info
        String osName = System.getProperty("os.name");
        String osVersion = System.getProperty("os.version");
        String osArch = System.getProperty("os.arch");

        System.out.println("==== System Info ====");
        System.out.println("OS: " + osName + " " + osVersion + " (" + osArch + ")");

        // CPU Info
        OperatingSystemMXBean osBean = ManagementFactory.getOperatingSystemMXBean();
        int availableProcessors = osBean.getAvailableProcessors();
        System.out.println("CPU Cores: " + availableProcessors);

        // Memory Info
        Runtime runtime = Runtime.getRuntime();
        long totalMem = runtime.totalMemory();
        long freeMem = runtime.freeMemory();
        long usedMem = totalMem - freeMem;
        long maxMem = runtime.maxMemory();

        System.out.println("\n==== Memory Info ====");
        System.out.printf("Used Memory: %.2f MB\n", usedMem / 1024.0 / 1024);
        System.out.printf("Free Memory: %.2f MB\n", freeMem / 1024.0 / 1024);
        System.out.printf("Total Memory: %.2f MB\n", totalMem / 1024.0 / 1024);
        System.out.printf("Max Memory (JVM limit): %.2f MB\n", maxMem / 1024.0 / 1024);

        // Disk Info
        File root = new File("/");
        long totalDisk = root.getTotalSpace();
        long freeDisk = root.getFreeSpace();
        long usableDisk = root.getUsableSpace();

        System.out.println("\n==== Storage Info ====");
        System.out.printf("Total Disk: %.2f GB\n", totalDisk / 1024.0 / 1024 / 1024);
        System.out.printf("Free Disk: %.2f GB\n", freeDisk / 1024.0 / 1024 / 1024);
        System.out.printf("Usable Disk: %.2f GB\n", usableDisk / 1024.0 / 1024 / 1024);
    }
}

