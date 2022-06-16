#!/bin/bash

declare -a toFetch;
declare -a ids;

for artifact in packages/* ; do
    for artifactVersion in ${artifact}/* ; do
      if [ -d "${artifactVersion}" ]; then
          if [ ! -f "${artifactVersion}/spec.json" ]; then
              echo "${artifactVersion}/spec.json does not exist";
              exit 0;
          else
              jarFiles=($(jq -r '.actions[] | select(.type == "one_step_deploy_plugin").arguments[] | select(.name == "jar").value' ${artifactVersion}/spec.json));
              configFiles=($(jq -r '.actions[] | select(.type == "one_step_deploy_plugin").arguments[] | select(.name == "config").value' ${artifactVersion}/spec.json));
              for jarFile in $jarFiles ; do
                  if [ ! -f "${artifactVersion}/${jarFile}" ]; then
                    if [ -f "${artifact}/build.yaml" ]; then
                        toFetch[${#toFetch[@]}]=${artifactVersion}/${jarFile}
                        ids[${#ids[@]}]="`yq eval '.maven-central.groupId' ${artifact}/build.yaml`:`yq eval '.maven-central.artifactId' ${artifact}/build.yaml`"
                    else
                        echo "${artifact}/build.yaml does not exist";
                        exit 0;
                    fi
                  fi
              done
              for configFile in $configFiles ; do
                  if [ ! -f "${artifactVersion}/${configFile}" ]; then
                      if [ -f "${artifact}/build.yaml" ]; then
                          toFetch[${#toFetch[@]}]=${artifactVersion}/${configFile}
                          ids[${#ids[@]}]="`yq eval '.maven-central.groupId' ${artifact}/build.yaml`:`yq eval '.maven-central.artifactId' ${artifact}/build.yaml`"
                      else
                          echo "${artifact}/build.yaml does not exist";
                          exit 0;
                      fi
                  fi
              done
          fi
      fi

    done
done

echo "Missing files before retrieval: "
for file in ${toFetch[@]} ; do
    echo $file;
done

for id in ${ids[@]} ; do
    echo $id;
done

i=0;
while [ $i -lt ${#toFetch[@]} ]; do
    filename=$(basename -- "${toFetch[$i]}")
    extension="${filename##*.}"
    json="$json{\"path\":\"${toFetch[$i]}\",\"target_path\":\"artifact/`echo "${toFetch[$i]}" | cut -d "/" -f 4`\",\"artifact\":\"`echo "${toFetch[$i]}" | cut -d "/" -f 4`\",\"repo\":{\"id\":\"${ids[$i]}\"\"version\":\"`echo "${toFetch[$i]}" | cut -d "/" -f 3`\",\"file_type\":\"${extension}\"}},";
    i=`expr $i + 1`;
done

output="[`echo $json | sed 's/.$//'`]"
echo $output

export output
echo "output=${output}" >> $GITHUB_ENV