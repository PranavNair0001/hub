#!/bin/bash

declare -a toFetch;
declare -a missing;

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
    fileName=`echo $file | cut -d "/" -f 4`;
    if [ -f "artifacts/${fileName}/${fileName}" ]; then
        mv artifacts/${fileName}/${fileName} $file
    else
        echo "$file : not retrieved"
    fi
done

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
                    missing[${#missing[@]}]=${artifactVersion}/${jarFile}
                fi
            done
            for configFile in $configFiles ; do
                if [ ! -f "${artifactVersion}/${configFile}" ]; then
                    missing[${#missing[@]}]=${artifactVersion}/${configFile}
                fi
            done
        fi
    done
done

echo "Missing files after retrieval: "
for file in ${missing[@]} ; do
    echo $file;
done
