for file in `cat test/bmc/BMC_journal_url.txt`
    do
        echo "Started" $file
        python3 src/bmc/bmc_url.py $file >> data/bmc/BMC_article_url.txt
        echo "Finished" $file

    done
