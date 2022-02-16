# K8 Přehled

## 00 Intro

### Co je to kubernet

* Platforma na správu aplikací v kontejnerech
* Hlídá stav běžících aplikací a automaticky se snaží řešit problémy
* Zajišťuje snadnou komunikaci mezi aplikacemi

### Linux

* cgroups
    * Omezují zdroje pro skupinu procesů.
    * Například množství RAM, vCPU, přístup k blokovým zařízením...
    * V k8s se typicky vážou na kontejner.
* namespace
    * Izolace skupin procesů
    * Například společný síťový stack, oddělení viditelnosti procesů, oddělení filesystému (něco jako chroot).
    * V k8s se některé aplikují na pod a některé na kontejner

## 01 Příprava pískoviště

* Přihlásit se na `user-profile.dev`
    * `kube-login all`
    * https://gitlab.seznam.net/ultra/SCIF/k8s/kube-login/-/releases
* Vytvořit namespace
    * `kubectl apply -f 01-playground/namespace.yaml`
* Natavit namespace jako výchozí
    * `kubectx`, `kubens`

## 02 Pod

* [Příklad podu](02-pod/pod.yaml)
    * `kubectl apply -f 02-pod/pod.yaml`
    * `kubectl get pods`
* Nejmenší možná konfigurace, která umožňuje provést výpočet.
* Obsahuje alespoň jeden kontejner (docker image).
* Dočasný immutable resource

## 03 Pod Controllers

* [ReplicaSet](03-controllers/01-replicaset.yaml)
    * Zajišťuje, že běží nastavený počet podů
    * Používá selector k "počítání" podů
    * Přímo se často nepoužívá
    * Pojmenování podů: `<ReplicaSet>-<PodId>`

* [Deployment](03-controllers/02-deployment-v1.yaml)
    * Bezstatové aplikace
    * Vytváří ReplicatSety, které vlastní pody
    * Nová konfigurace aktivuje (ve výchozím stavu) RollingUpdate:
        * Pody v replicasetu se postupně ukončují a nahrazují novou instancí
        * Starý replicaset běží dokud neběží nový replica set
        * Možnost vrátit se ke starému replica setu
            * `kubectl rollout undo deployment <deployment>`
    * Pojmenování podů: `<Deployment>-<ReplicaSet>-<PodId>`

* [StatefulSet](03-controllers/03-statefulset.yaml)
    * Bez replica setů
    * Vlastní pody
    * Pod si zachovává
        * síťovou identitu (nezáleží na počtu restartů vždy bude mít stejný hostname)
        * storage identitu (poze při použití PVC, vždy dostane stejný storage)
    * Vyžaduje *Headless Service*.
    * Pojmenování podů: `<StatefulSet>-<counter>`

* [DaemonSet](03-controllers/04-daemonset.yaml)
    * vlastní pody
    * Zajistí spuštění podů na každém nodu v clusteru
    * Pozor na tainty (omezení nastavené na Nodu určující co na něm může běžet)
    * Užitečné s `HostPath`
    * Pojmenování podů: `<DaemonSet>-<PodId>`

* [Job](03-controllers/05-job.yaml)
    * Vlastní pody
    * Spustí sekvenčně nebo paralelně pody
    * Pojmenování podů: `<Job>-<PodId>`
    * Joby a Pody zůstavají v K8s po skončení pro check logů
        * TTL mechanismus pro úklid
    * Např. batchové zpracování dat z front

* CronJob
    * Spuští Job v pravidelných intervalech

## 04 Komunikace

### Mezi kontejnery v jednom podu

* Volumes
    * Sdílený adresář
    * Soubory
    * UNIX socket
    * Pipe
* Persistent Volume Claim (PVC)
    * Storage v podobě filesystému, který přežije vypnutí podu
* Network
    * Všechyn kontejnery v podu sdílí namespace -> localhost
    * Pozor na stejné porty
* Signály
    * Procesy na sebe musí vidět -> stejný
      namespace, [musí se explicitně zapnout](https://kubernetes.io/docs/tasks/configure-pod-container/share-process-namespace/)

### Mezi pody

* Vyžaduje se [Service](04-communication/01-communication.yaml) (`kubectl get services`)
    * Service má vlastní IP
    * Vytvoření service -> vytvoří endpointy s IP podů (`kubectl get endpoints`)
    * Pody pak směřují na IP service z ní se provede překlad na konkrétní pod
* Persistent Volumes
    * Sdílí se část filesystému, např přes S3
    * Vhodné pro velmi obskurdní případy

### Zvenku na pod

* Ingress
    * Nečastěji se jedná o NGINX, který je běží v kubernetu
    * Provoz na servicy směčuje podle doménového jména
    * Potřeba záznam v DNS manageru
        * V user-profile-dev.ko např. `hello.dev.k8s.cileni.dszn.cz CNAME user-profile-dev.ko.k8s.scif.cz`
    * Vhodné pro debug interních služeb, nebo služby s velmi nízkým provozem (např. web interface Arga)

* [Labrador](04-communication/01-communication-labrador.yaml)
    * Vyžaduje alokaci IP adresy
        * V provozu od adminů
        * V devu stačí přidat si svoji službu v https://gitlab.seznam.net/ultra/SCIF/labrador/dev-ip-allocation
    * Váže se na `Service`
    * Vyžaduje
      specifické [anotace](https://gitlab.seznam.net/ultra/SCIF/labrador/documentation/-/blob/master/kubernetes_reference.md)
    * Potřeba záznam v DNS manageru
        * Záznam na konkrétní IP adresu, např. `hello-labrador.dev.k8s.cileni.dszn.cz A 10.32.252.79`
    * TLS stačí vygenerovat v [TLS manageru](https://tls.seznam.net/ca/)
      * V produkci žádají admini
      * Pro dev je možné zažádat přímo o cert podepsaná [Seznam CA](https://tls.seznam.net/ca/13/)

## 05 Konfigurace

* ConfigMap
    * Umožňuje držet konfiguraci mimo aplikaci
    * Manifest obsahující seznam klíčů s hodnotou
    * Hodnota pro každý klíč může být
        * Mountuta jako soubor do filesystmu kontejneru
        * Předána jako proměnná prostředí
        * Kombinace předchozího
    * Pokud se změní ConfigMap, Pod který ji používá se automaticky **nerestartuje**
        * Mountnutý soubor v Podu se upravý
* Environment
    * Jsou součástí definice podu
    * Změna a naszení vedek *restartu* podu
* Secrets
    * Podobná struktura jako u ConfigMapy
    * Vlastní resource, umožňuje řídit přístup k nim v kubernetu
    * Secrety mohou být syncované ze sasanky

# Co dál?

## Pod lifecycle

* Readiness
* Liveness
* Startup

## Automatické škálování podů

* Horizontal
* Vertical
* Cluster

## Persistent Volumes

* Co to je
* Jak to získat
* Jak to použít

## Nodes

* Alokace
* Správa nodů

## Authentifikace služeb

* Role
* Binding
* Accounts

## Internals

### Z čeho se kubernetes skládá

* API
* etcd
* controller manager
* kubelet
* scheduler

### Pod internals

* `pause` container
* jaké namespaces se sdílí a jak to zjistit

### Jak funguje load balancing v K8s

* user-space
* iptables
* virtual server

## Kustomize

* Co to je
* Jak to použít
