#!/bin/bash

declare -a toFetch;
declare -a urls;

for artifact in packages/* ; do
    for artifactVersion in ${artifact}/* ; do
        if [ ! -f "${artifactVersion}/spec.json" ]; then
            echo "${artifactVersion}/spec.json does not exist";
            exit 0;
        else
            jarFiles=($(jq -r '.actions[] | select(.type == "one_step_deploy_plugin").arguments[] | select(.name == "jar").value' ${artifactVersion}/spec.json));
            configFiles=($(jq -r '.actions[] | select(.type == "one_step_deploy_plugin").arguments[] | select(.name == "config").value' ${artifactVersion}/spec.json));
            for jarFile in $jarFiles ; do
                if [ ! -f "${artifactVersion}/${jarFile}" ]; then
                    toFetch[${#toFetch[@]}]=${artifactVersion}/${jarFile}
                    urls[${#urls[@]}]=`jq -r '.actions[] | select(.type == "one_step_deploy_plugin").arguments[] | select(.name == "repo_url").value' ${artifactVersion}/spec.json`
                fi
            done
            for configFile in $configFiles ; do
                if [ ! -f "${artifactVersion}/${configFile}" ]; then
                    toFetch[${#toFetch[@]}]=${artifactVersion}/${configFile}
                    urls[${#urls[@]}]=`jq -r '.actions[] | select(.type == "one_step_deploy_plugin").arguments[] | select(.name == "repo_url").value' ${artifactVersion}/spec.json`
                fi
            done
        fi
    done
done

for file in ${toFetch[@]} ; do
    echo $file;
done

for url in ${urls[@]} ; do
    echo $url;
done

i=0;
while [ $i -lt ${#toFetch[@]} ]; do
    json="$json{\"path\":\"${toFetch[$i]}\",\"target_path\":\"target/${toFetch[$i]}\",\"repo\":{\"url\":\"${urls[$i]}\",\"owner\":\"`echo ${urls[$i]} | cut -d "/" -f 4`\",\"repo\":\"`echo ${urls[$i]} | cut -d "/" -f 5`\",\"tag\":\"v`echo ${toFetch[$i]} | cut -d "/" -f 3`\",\"checkout\":\"`echo ${urls[$i]} | cut -d "/" -f 4-5`\"}},";
    i=`expr $i + 1`;
done

output="[`echo $json | sed 's/.$//'`]"
echo $output

export output
echo "output=${output}" >> $GITHUB_ENV