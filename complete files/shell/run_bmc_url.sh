for file in `cat BMC_journal_url.txt`
    do
        echo "Started" $file
        python3 bmc_url.py $file >>BMC_article_url.txt
        echo "Finished" $file

    done
