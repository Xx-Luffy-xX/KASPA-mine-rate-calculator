# KASPA-mine-rate-calculator
A calculator for mining rate of Kaspa currency.

## Instructions:
Just place the file in the kaspa directory (where kaspactl is located) and run (preferably from terminal/cmd/powershell).

Example: `./kas-rate-linux`.

OPTIONAL: use "-s" flag to specify IP address of a public node.

Example: `./kas-rate-linux -s 10.0.0.38`

## How it works:
The code uses kaspactl to pull the current global hash-rate, then asks for the local (user's) hash-rate and calculates the mining-rate in terms of blocks and KAS.

Source code was written in python and compiled using pyinstaller package. You may download it, change it and recompile if you like.

### Donations will be welcom at:
kaspa:qzhxqtue7rq6r64vuvhxq3athj6jxj2kx6e94xdgc9ugt8ry34ptsnvst6cym

Cheers!
