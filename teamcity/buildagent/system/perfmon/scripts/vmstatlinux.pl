#!/usr/bin/perl -w
use strict;
use POSIX;

# output file
my $out;
# memory monitoring
my $vmd;

my $outfile = $ARGV[0];
my $delay = $ARGV[1];
my $delaySec = $delay / 1000;

$SIG{'INT'} = "termination";
$SIG{'TERM'} = "termination";
$SIG{'ABRT'} = "termination";
$SIG{'KILL'} = "termination";
$SIG{'QUIT'} = "termination";

open($out, ">$outfile");
{
  my $ofh = select $out;
  $| = 1;
  select $ofh; # disable buffering
}

my $freeMem = 0;
my $maxFreeMem = 0;
my $cpuTime = cpu_time_millis();
my $diskTime = disk_time_millis();
my $ramSize = ram_size();

print $out "Date/Time, % CPU Time, % Disk Time, % Used memory, % Used agent RAM, RAM size (bytes)\n";
my $v = open($vmd, '-|', 'vmstat', $delaySec) or die("Can't start vmstat command: $!");

my $line;
while(1) {
  $line = <$vmd>;
  if (defined $line) {
    $line = trim($line);
    if ($line =~ /[0-9]+\s+[0-9]+.*/) {
      my @vals = split(/\s+/, $line);
      if ($#vals < 15) {next;}
      $freeMem = $vals[3] + $vals[4] + $vals[5];
      if ($freeMem > $maxFreeMem) {
        $maxFreeMem = $freeMem;
      }

      my $cpuUsage = 100 - $vals[14];

      my $usedMem = round(100.0 * ($maxFreeMem - $freeMem) / ($maxFreeMem + 1));

      my $cpuEndTime = cpu_time_millis();
      my $diskEndTime = disk_time_millis();

      my $diskTimeSpent = $diskEndTime - $diskTime;
      my $cpuTimeSpent = $cpuEndTime - $cpuTime;

      $cpuTime = $cpuEndTime;
      $diskTime = $diskEndTime;

      my $usedAgentRam;
      my $ramSizeBytes;

      if ($ramSize != -1) {
        $usedAgentRam = round(100 * ($ramSize - $freeMem) / ($ramSize + 1));
        $ramSizeBytes = $ramSize * 1024;  # kb
      } else {
        $usedAgentRam = -1;
        $ramSizeBytes = -1;
      }

      if ($cpuTimeSpent > 0) {
        my $diskUsage = round(100.0 * $diskTimeSpent / 1000);
        if ($diskUsage > 100) {
          $diskUsage = 100;
        }
        my $time = 1000 * time();

        printf $out "%s, %d, %d, %d, %d, %d\n", $time, $cpuUsage, $diskUsage, $usedMem, $usedAgentRam, $ramSizeBytes;
      }
    }
  } else {
    die("Failed to read vmstat output. Performance monitoring data can be inaccurate\n");
  }
}
termination();

sub disk_time_millis {
  my $res = 0;
  open(DSD, "< /proc/diskstats") or die("Can't open /proc/diskstats file: $!");
  while (my $l = <DSD>) {
    # parse stats for both regular hd$/sd$ disks and nvme ones
    if ($l =~ /\s+[0-9]+\s+[0-9]+\s+([a-z]+|nvme[0-9]+n[0-9]+)\s+.*/) {
      my @vals = split(/\s+/, $l);
      # Linux kernel v4.19 reports 18 values. we need 13th (time spent doing I/Os (ms))
      if ($#vals >= 13) {
        $res += int($vals[13]);
      }
    }
  }
  close(DSD);

  return $res;
}

sub cpu_time_millis {
  my $total = 0;
  open(PSD, "< /proc/stat") or die("Can't open /proc/stat file: $!");
  while (my $l = <PSD>) {
    if ($l =~ /cpu\s+([0-9]+).*/) {
      my @vals = split(/\s+/, $l);
      for (my $i = 1; $i <= $#vals; $i++) {
        $total += int($vals[$i]);
      }
    }
  }
  close(PSD);
  return $total * 10; # millis
}

sub ram_size {
  open(MSD, "< /proc/meminfo") or return -1;
  my $ram = <MSD>;
  if (not defined $ram) {
    die("Failed to read available RAM size on agent. Performance monitoring data can be inaccurate");
  }
  $ram =~ s/\D//g;
  close(MSD);
  return $ram;
}

sub round {
  return int($_[0] + 0.5);
}

sub trim {
  my $s = shift;
  $s =~ s/^\s+|\s+$//g;
  return $s
};

sub termination {
  kill TERM => $v;
  close($out) or die ("Cannot close perfmon output");
  exit 0;
}
