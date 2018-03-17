for file in `cat test/indjst_url.txt`
    do
        echo "Started" $file
        python3 src/indjst_parser.py $file
        echo "Finished" $file
        sleep 1s
    done
