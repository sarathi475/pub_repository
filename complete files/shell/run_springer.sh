for file in `cat springer/springer_all_volume.txt`
    do
        echo "Started" $file
        python3 springer/springer_parser.py $file
        echo "Finished" $file
    done
