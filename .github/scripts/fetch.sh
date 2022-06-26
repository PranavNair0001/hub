echo "Fetching: ${FILEPATH}"

if [ -f "${FILEPATH}" ]; then
    echo "${FILENAME} : Found in GCS Bucket"
    mkdir "artifact"
    cp ${FILEPATH} artifact/
else
    echo "${FILENAME} : Not found in GCS Bucket, Fetching from Maven Central"
    mvn org.apache.maven.plugins:maven-dependency-plugin:2.8:copy -Dartifact=${ID}:${VERSION}:${EXTENSION} -DoutputDirectory=./artifact/
fi