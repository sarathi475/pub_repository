for file in `cat test/bmc/BMC_article_url.txt`
    do
        echo "Started" $file
        python3 src/bmc/bmc_parser.py $file
        echo "Finished" $file
    done
