# Task 2 - Log analysis

## Request counts

1. **Get the count of GetTemporaryAuthenticationTokenRequest from the log**

        zstdgrep -c "GetTemporaryAuthenticationTokenRequest" /opt/local/logs/server.log.gz

    **Expected output:**

        14823

1. **Get count of LoginRequests per minute**

        zstdgrep 'LoginRequest' /opt/local/logs/server.log.gz | awk -F':' '{print $1}' | sed 's/^I //' | sort | uniq -c | awk '{print $1, $2, $3}'
    **Expected output:**

        636 0114-1145
        1400 0114-1146
        1400 0114-1147
        1400 0114-1148
        1400 0114-1149
        1400 0114-1150
        1400 0114-1151
        1400 0114-1152
        1400 0114-1153
        1400 0114-1154
        1400 0114-1155
        186 0114-1156

1. **List all requests (and their counts) that had JSON OUT: string in it**

        zstdgrep ' JSON OUT: ' /opt/local/logs/server.log.gz | awk -F' ' '{print $6}' | awk -F'\\(' '{print $1}' | sort | uniq -c
    **Expected output:**

        14823 GetTemporaryAuthenticationTokenRequest-31284
        14822 LoginRequest-31280

## Parse data

**For request/response with id 149418, get values for obj=, ipAddress=, customData=[KV(5, playerCode= and flow= in one line**

    target=$(zstdgrep '149418' /opt/local/logs/server.log.gz)
    obj=$(echo "$target" | grep -E -o 'obj=([^,]*)' | awk -F'=' '{print $2}' | tr -d '\\')
    ipAddress=$(echo "$target" | grep -E -o 'ipAddress=([^,]*)' | awk -F'=' '{print $2}' | tr -d '\\')
    hash=$(echo "$target" | grep -E -o '#([^)]*)')
    playerCode=$(echo "$target" | grep -E -o 'playerCode=([^,]*)' | awk -F'=' '{print $2}' | tr -d '\\')
    flow=$(echo "$target" | grep 'LoginResponse' | grep -E -o 'flow=([^,]*)\)' | tr -d '\)' | sed 's/flow=//')
    echo $obj $ipAddress $hash $playerCode $flow

**Expected output:**

    PT04LOGIN49756-playtech93004, 10.144.227.18, #webVent, 58619722, 250168855196269516:2

## Bonus

**Get the duration= of all requests, summed up**

    echo $(zstdgrep 'duration=' /opt/local/logs/server.log.gz | grep -o 'duration=[0-9.]*' | awk -F'=' '{print $2}' | paste -sd+ - | bc) "(milliseconds)"
**Expected output:**

    608740 (milliseconds)
