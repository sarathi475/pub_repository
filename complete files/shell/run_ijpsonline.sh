for file in `cat ijpsonline_url.txt`
    do
        echo "Started" $file
        python3 ijpsonline_parser.py $file
        echo "Finished" $file
    done
