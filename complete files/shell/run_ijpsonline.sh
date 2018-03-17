for file in `cat test/ijpsonline_url.txt`
    do
        echo "Started" $file
        python3 src/ijpsonline_parser.py $file
        echo "Finished" $file
    done
