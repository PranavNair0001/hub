#!/bin/bash

declare -a toFetch;

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
                fi
            done
            for configFile in $configFiles ; do
                if [ ! -f "${artifactVersion}/${configFile}" ]; then
                    toFetch[${#toFetch[@]}]=${artifactVersion}/${configFile}
                fi
            done
        fi
    done
done

for file in ${toFetch[@]} ; do
    echo $file;
done

for file in ${toFetch[@]} ; do
    json="$json{\"path\":\"$file\"},";
done

output="[`echo $json | sed 's/.$//'`]"
echo $output

export output
echo "output=${output}" >> $GITHUB_ENV