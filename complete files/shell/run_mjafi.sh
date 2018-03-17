for file in `cat test/mjafi_url.txt`
    do
        echo "Started" $file
        python3 src/mjafi_parser.py $file
        echo "Finished" $file

    done
