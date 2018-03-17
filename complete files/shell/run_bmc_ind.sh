for file in `cat test/bmc_ind_url.txt`
    do
        echo "Started" $file
        python3 src/bmc_ind_parser.py $file
        echo "Finished" $file
        sleep 1s
    done
