for file in `cat ias_art_url.txt`
    do
        echo "Started" $file
        python3 ias_parser.py $file 
        echo "Finished" $file

    done
